#!/bin/bash
#
# Helper script to run examples
#

if [ -z "$1" ]; then
    echo "Usage: ./run_example.sh [example_name]"
    echo ""
    echo "Available examples:"
    echo "  default      - Task management app (inputs/sample_taskmgmt.txt)"
    echo "  ecommerce    - E-commerce platform (inputs/sample_ecommerce.txt)"
    echo "  healthcare   - Telemedicine platform (inputs/sample_healthcare.txt)"
    echo "  custom       - Specify custom file path"
    echo ""
    echo "Examples:"
    echo "  ./run_example.sh default"
    echo "  ./run_example.sh ecommerce"
    echo "  ./run_example.sh custom inputs/my_requirements.txt"
    exit 1
fi

case "$1" in
    default)
        echo "Running default example (Task Management App)..."
        crewai run
        ;;
    ecommerce)
        echo "Running e-commerce example..."
        INPUT_FILE=inputs/sample_ecommerce.txt crewai run
        ;;
    healthcare)
        echo "Running healthcare example..."
        INPUT_FILE=inputs/sample_healthcare.txt crewai run
        ;;
    custom)
        if [ -z "$2" ]; then
            echo "Error: Please specify input file path"
            echo "Usage: ./run_example.sh custom inputs/your_file.txt"
            exit 1
        fi
        echo "Running custom example: $2"
        INPUT_FILE="$2" crewai run
        ;;
    *)
        echo "Unknown example: $1"
        echo "Use: default, ecommerce, healthcare, or custom"
        exit 1
        ;;
esac

